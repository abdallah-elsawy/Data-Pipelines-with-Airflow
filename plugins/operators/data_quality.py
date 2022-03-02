from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    To check the data quality by running a sql_query
             
    """

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 dq_checks=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)

        self.check = dq_checks
        self.redshift_conn_id = redshift_conn_id

        
        
        
        
    def execute(self, context):
    	redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
    	for table in self.tables:
            results = redshift.get_records("SELECT COUNT(*) FROM {}".format(table))
            count = len(results)
            count_0 = len(results[0])
            
            if count  < 1 or count_0 < 1 :
                raise ValueError(f"DataQualityOperator implemented")
                
            self.log.info('DataQualityOperator passed')        
        

#     def execute(self, context):
#     	redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

#         for check in self.dq_checks:
#             sql = check.get('check_sql')
#             exp_result = check.get('expected_result')

#             records = redshift.get_records(sql)[0]
#             num_records = records[0][0]
#             if num_records != exp_result:
#                 raise ValueError(f"DataQualityOperator failed")
#             else:
#                 self.log.info(f"Data quality on passed")              
