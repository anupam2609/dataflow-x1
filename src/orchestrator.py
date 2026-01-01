import yaml
import os
from src.engines.python_engine import EngineFactory


def run_etl_pipeline():
    # Load configuration
    config_path = os.getenv('ETL_CONFIG_PATH', '/opt/spark/work-dir/config/etl_settings.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    mode = config.get('execution_mode', 'snowflake')
    settings = config.get('snowflake_pipeline', {})

    # Initialize Engine
    engine = EngineFactory.get_engine(mode)

    # 1. Transform (SQL Push-down)
    if settings.get('transform') and settings.get('transformation_query'):
        query = settings['transformation_query'].format(
            target_table=settings['target_table'],
            source_table=settings['source_table']
        )
        engine.transform(query)

    # 2. Read (Optional local processing)
    if settings.get('read'):
        df = engine.read(f"SELECT * FROM {settings['target_table']} LIMIT 10")
        print("Sample Data Preview:")
        print(df.head())


if __name__ == "__main__":
    run_etl_pipeline()