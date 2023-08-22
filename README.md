Async REST API for a restaurant menu. Implemented 3 entities: Menu, Submenu, Dish.

Dependencies:
- A menu has submenus that are linked to it.
- The submenu has dishes that are linked to it.

Implemented caching. Redis is used as a cache storage.

Technology stack:

```Python``` ```FastAPI``` ```PostgreSQL``` ```Docker``` ```Pytest``` ```Redis```

Application launch:
 - clone the repository
 - go to project folder

    ```
    cd restaurant-menu-fastapi/
    ```
 - running app:

    ```
    docker-compose up -d
    ```
 - running tests:

    ```
    docker-compose -f docker-compose-tests.yaml up
    ```

Documentation is available at the link: http://127.0.0.1:8000/docs
