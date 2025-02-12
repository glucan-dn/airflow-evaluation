import logging
 
def start_task():
    logging.info("Workflow has started.")

def decide_branch(**kwargs):
    # Access data_type from the DAG run configuration
    data_type = kwargs.get('dag_run').conf.get('data_type', 'sales')
    logging.info(f"Data type selected: {data_type}")
    
    if data_type == 'sales':
        return 'process_sales'
    elif data_type == 'inventory':
        return 'process_inventory'
    elif data_type == 'marketing':
        return 'process_marketing'
    else:
        return 'unknown_data_type'
    
def process_sales():
    logging.info("Processing sales data.")

def process_inventory():
    logging.info("Processing inventory data.")

def process_marketing():
    logging.info("Processing marketing data.")

def unknown_data_type():
    logging.warning("Unknown data type provided. No processing will be done.")

def end_task():
    logging.info("Workflow has completed.")