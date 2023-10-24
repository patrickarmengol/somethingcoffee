# somethingcoffee

website for discovering specialty coffee shops

> disclaimer: This project is in its early stages. The site is not yet publicly accessible.

---

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

Set up a `.env` file with the following environment variables:

- `DB_URL` - should use `db` for the hostname
- `POSTGRES_USER`
- `POSTGRES_PASS`
- `POSTGRES_DBNAME`

Then run the docker-compose to build the images and run the containers, passing in the env file.

```
docker-compose up -d --build
```

The asgi server should wait for the database to start before running.

## Usage

### Site URL

http://localhost:5000

### API Docs URL

http://localhost:5000/schema/swagger

## License

The source code for `somethingcoffee` is distributed under the terms of any of the following licenses:

- [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html)
- [MIT](https://spdx.org/licenses/MIT.html)

The content on the site is distributed under:

- [CC BY NC SA 4.0](https://spdx.org/licenses/CC-BY-NC-SA-4.0.html)
