# Database Management Module (db_management)

## Introduction

The db_management module constitutes a vital part of the project, acting as a conduit for all database-related operations. It offers a flexible, performant, and thread-safe approach to manage connections, execute queries, orchestrate transactions, and define schemas. This document elucidates the technical architecture, class interactions, usage examples, and thread safety considerations. Starting from the overview of the classes


## Architecture Overview

### Class Diagram


      +-----------------------+
      | RDBConnectionWrapper  |
      +-----------------------+
                |
                v
      +-----------------------+
      |    RDBQueryExecutor   |
      +-----------------------+
                |
                v
      +-----------------------+
      |   RDBSchemaBuilder    |
      +-----------------------+
                |
                v
      +-----------------------+
      |      RDBManager       |
      +-----------------------+
                |
                v
      +-----------------------+
      |       RDBHelper       |
      +-----------------------+
                |
                v
      +-----------------------+
      |  RDBHelperFactory     |
      +-----------------------+

## Class Descriptions

1. **DBConfig**
2. **RDBConnectionWrapper**
3. **RDBQueryExecutor**
4. **RDBSchemaBuilder**
5. **RDBManager**
6. **RDBHelper**
7. **RDBHelperFactory**


## Example Usage

    # config = DBConfig((**load_db_env()))
    # db_wrapper = RDBConnectionWrapper(config)
    # db_schema_builder = RDBSchemaBuilder()
    # db_manager = RDBManager(db_wrapper, db_schema_builder)
    # db_helper = RDBHelper(db_manager)
    # db_helper.fetch_stuff
    #   Above using the factory pattern
    #   e.g.,:
    #   db_helper = RDBHelperFactory.create_helper(DBType.POSTGRES, config)
...
...
...



# Thread Safety

- Connection Pooling: 
  - Utilizes psycopg2's ThreadedConnectionPool to ensure thread-safe connection management.
      
- Transaction Isolation: 
  - Adheres to transaction isolation principles to maintain integrity across concurrent threads.

# Extensibility

- Database Compatibility: 
  - Designed for seamless adaptability to various RDBMS.
    
- Schema Flexibility: 
  - Schema can be effortlessly extended or altered via RDBSchemaBuilder.

# Conclusion

...

# TL;DR (Too Long; Didn't Read)

...