
#https://astronomer-providers.readthedocs.io/en/1.18.4/_modules/airflow/utils/context.html
from airflow.operators.email_operator  import EmailOperator

from airflow.utils.decorators import apply_defaults
class DynamicRecipientsEmailOperator(EmailOperator):
    #db_conn_id will tell what db to pull recipient emails from
    #type - Emails are looked up by airflow-ID*, then more granular searching by type. 
        #Would be useful if want to send to the "default" group in every case besides failure.
        #If a dag fails, maybe send email to "type"=="failure"

        #*airflow-ID isn't explicitly written out in params because it's contained in Context which
        #is passed in through **kwargs
    def __init__(self, *, db_conn_id:str="sqlite:///recipients.db", flag_id="DEFAULT", **kwargs):
        #Remove to, bcc, and cc fields if passed. This is to make explcitlity clear that these fields
        #are not supposed to be explicitly passed in. Rather, dynamically pulled from db
        kwargs.pop("to",None)
        kwargs.pop("bcc",None)
        kwargs.pop("cc",None)
        self.flag_id = flag_id
        super().__init__(to=[], bcc=[], cc=[], **kwargs)
        self.db_conn_id = db_conn_id
    
    def execute(self, context:dict):
        if type(context) is not dict:
            raise TypeError("context in DynamicRecipientsEmailOperator is not of type dict")

        dag_id = context['dag_run'].dag_id
        task_id = context['ti'].task_id
        
        #Overwrite the recipient attributes with the dynamically fetched list
        #self.to = 
        #self.bcc = 
        #self.cc = 
        super().execute(context)



    