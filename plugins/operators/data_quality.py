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
                 tables=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)

        self.tables = tables
        self.redshift_conn_id = redshift_conn_id


    def execute(self, context):
    	redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
    	for table in tables:
            
	    results = tables[table][1]
	    for result in results:
                
                count = redshift.get_records(result)[0][0]
		if count != results[result]:
                    
		   raise ValueError(f"DataQualityOperator not implemented yet")
            
            self.log.info('DataQualityOperator passed')
