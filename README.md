# KnowAfrika API
***Accessible API to know Africa***

![knowafrika_113603](https://github.com/samuelselasi/KnowAfrika-API/assets/85158665/c996a1d4-dea7-45e3-9068-7974aeb065e3)

## Content

* [About](#about)
* [Installation](#installation)
* [Usage](#usage)
* [Features](#features)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)

## About

The inception of the `KnowAfrika` API was motivated by
our aspiration to offer a solution focused on acquiring
a deeper understanding of Africa through an `API` service.

We firmly believe in the transformative potential of
technology to democratize information.

Our overarching mission is to enhance the accessibility
of information about Africa, making it readily available
to individuals not only across the continent but
also worldwide.

## Installation

Refer to [backend](./backend) directory for
detailed information on installation and environment requirements


## Usage

### API Access
* **Base url** -> `http://127.0.0.1:8000`
* **SWagger  docs** -> `http://127.0.0.1:8000/docs`

### API Requests
* **Curl** -> On command terminal
* **Browser** 

***find out more in [technical documentation](./frontend/web_static/tech_doc.html) page***

## Features

| Feature | 	Description | Directory |
| --- | --- | --- |
| Landing Page | Page containing information on the project and contacts of contributers | [Web Static](./frontend/web_static/index_html) |
| Technical Documentation Page | Page containing technical documentation of API | [Web Static](./frontend/web_static/tech_doc.html) |
| User Modules | Router containing endpoints with CRUD functions on `User` modules | [Users](./backend/app/routers/user) |
| Authentication | Router containing endpoints with CRUD functions on user `authentication` | [Authentication](./backend/app/routers/auth) |
| Regions | Router containing endpoints with CRUD functions on `regions` of Africa | [Users](./backend/app/routers/regions) |
| Countries | Router containing endpoints with CRUD functions on African `countries` | [Countries](./backend/app/routers/countries) |
| Provinces | Router containing endpoints with CRUD functions on `provinces` of African countries | [Provinces](./backend/app/routers/provinces) |
| Cities | Router containing endpoints with CRUD functions on `cities` of provinces in African countries | [Cities](./backend/app/routers/cities) |
| Flags | Router containing endpoints with CRUD functions on `falgs` of African countries  | [Flags](./backend/app/routers/flags) |
| Currencies | Router containing endpoints with CRUD functions on `currencies` of African countries | [Currencies](./backend/app/routers/currencies) |
| Languages | Router containing endpoints with CRUD functions on `languages` of African countries | [Languages](./backend/app/routers/languages) |
| Time-zones | Router containing endpoints with CRUD functions on `time-zones` of African countries | [Time-zones](./backend/app/routers/timezones) |
| Transport | Router containing endpoints with CRUD functions on `transportation` modes of African countries | [Transportation](./backend/app/routers/transport) |
| Constitutions | Router containing endpoints with CRUD functions on `constitutions` of African countries | [Constitutions](./backend/app/routers/constitutions) |


## Contributing
##### Main Branch
The `main` branch represents the main
codebase and should always contain stable
and production-ready code. Developers
should avoid directly committing
changes to this branch to maintain
its integrity.

##### Feature Branches
When working on a new feature, bug fix,
or improvement, developers create a new
branch from the "main" branch.
This branch is often named after the
feature or issue being addressed.

##### Code Development
Developers work in their respective feature
branches to implement and test the
changes related to their assigned
tasks. Frequent commits are made to
track progress.

##### Pull Requests (PRs)
Once a feature or bug fix is complete,
the developer creates a pull request
from their feature branch to the `master`
branch. The pull request includes a
summary of changes, the purpose of the
code, and any relevant details.

##### Code Review
Team members or designated reviewers review
the code changes in the pull request. They
provide feedback, suggest improvements,
and ensure code quality and best practices.

##### Continuous Integration (CI)
Automated tests and checks are run as part
of the CI process to verify that the new code
integrates smoothly with the existing
codebase and passes all necessary tests.

##### Merging
After the pull request is approved and any
requested changes are addressed, the code
is merged into the `master` branch. This
integration brings the new feature or
fix into the main codebase.

##### Tagging and Releases
Once a set of features or bug fixes is
merged into the `master` branch, a
release may be created by tagging the
commit with a version number. This
helps track and manage different
versions of the software.

##### Branch Cleanup
After successful merging, feature
branches are usually deleted to keep
the repository organised and avoid
clutter.

***By following this branching and merging process,
teams can collaborate effectively, maintain a stable
main codebase, and ensure that new code additions
are well-tested and thoroughly reviewed before
becoming part of the production code.***

## License
#### This project is licensed under the MIT License - see [LICENSE](./LICENSE) for details.

## Authors

1. [Samuel Selasi K.](https://github.com/samuelselasi) -> [Linkedin](https://www.linkedin.com/in/samuel-selasi-kporvie), [Medium](https://medium.com/@onepunchcoder), [X](https://medium.com/@onepunchcoder)

2. [Stacy Gakiria](https://github.com/SKGakiria) -> [Linkedin](), [Medium](), [x]()

