import pandas as pd
import numpy as np

class Cohort():
    # for calculating the cohort filter by segments in the front-end
    @staticmethod
    def count_cohort_segments(df, frequency):
        # Generate continuous time series
        time_series = pd.date_range(start=min(df['date']), end=max(df['date']), freq=frequency)
        time_series_df = pd.DataFrame({'date': time_series})

        # Get unique user_id values from df
        unique_user_ids = df['user_id'].unique()
        unique_user_ids_df = pd.DataFrame({'user_id': unique_user_ids})

        # Get unique segments
        unique_segment = df['segment'].unique()
        unique_segment_df = pd.DataFrame({'segment': unique_segment})

        # Perform cross join with time_series_df
        df_cross_join = pd.merge(pd.merge(unique_user_ids_df, time_series_df, how='cross'), unique_segment_df, how='cross')

        # Attach cohort column
        df_cont = pd.merge(df_cross_join, df, how='left', on=['user_id', 'date', 'segment'])
        df_cont['count'].fillna(0, inplace=True)
        df_created = df.groupby(['user_id'])['date'].min().reset_index().drop_duplicates()
        df_created.columns = ['user_id', 'created']
        df_cont_created = pd.merge(df_cont, df_created, how='left', on=['user_id'])

        # Handle the frequency
        if frequency == 'MS':
            df_cont_created['cohort'] = (df_cont_created['date'].dt.to_period('M') - df_cont_created['created'].dt.to_period('M')).apply(lambda r: r.n) * df_cont_created['count']
        else: 
            df_cont_created['cohort'] = (df_cont_created['date'].dt.to_period('W') - df_cont_created['created'].dt.to_period('W')).apply(lambda r: r.n) * df_cont_created['count']

        df_cont_created['cohort'] = df_cont_created['cohort'].astype(int).astype(str)
        df_cont_created.loc[df_cont_created['count'] != 0.0, 'cohort'] = 't' + df_cont_created['cohort']
        df_cont_created.drop(df_cont_created[df_cont_created['cohort'] == '0'].index, inplace=True)

        result = df_cont_created.groupby(['created', 'cohort', 'segment']).size().reset_index(name='count')

        # refine the results if dataset too sparse
        indexes_df = pd.DataFrame({'cohort': np.arange(len(time_series_df))})
        cross_join_df = pd.merge(pd.merge(time_series_df, indexes_df, how = 'cross'), unique_segment_df, how = 'cross')
        cross_join_df['cohort'] = 't' + cross_join_df['cohort'].astype(int).astype(str)
        cross_join_df.rename(columns={'date': 'created'}, inplace=True)
        refined_result = pd.merge(cross_join_df, result, how='left', on=['created', 'cohort', 'segment'])
        return refined_result

    # to convert the values to percentages
    @staticmethod
    def to_pct(result):
        subset = result[result['cohort'] == 't0']
        result_t0 = pd.merge(result, subset, how='left', on=['created', 'segment'])
        result_t0.loc[result_t0['count_y'].notnull(), 'pct'] = result_t0['count_x']/result_t0['count_y']
        result_t0.drop(['count_x', 'cohort_y', 'count_y'], axis=1, inplace=True)
        return result_t0

    # to generate the values cohort when calculating kWhs/££
    # @staticmethod
    # def value_cohort(df):