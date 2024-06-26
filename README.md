
Note April/24/2024: I have checked and this version is still compatible with chainlit version 1.0.505. If You have any error please let me know. I will continue monitoring chainlit versions to see when we need an update for a new Docker image

# ChainLit Chat History Persister

[![Example Using Chainlit Custom Server]](https://youtu.be/S6AR5shbcZc?si=Y9zGDGcjJJYccaKs)


:warning:**Disclaimer**: This project is an independent, open-source initiative aimed at persisting chat history for ChainLit users. It is **not** officially affiliated with, endorsed by, or related to the ChainLit project or its developers. While every effort is made to ensure accuracy and compatibility, the nature of open-source work means that we cannot guarantee absolute compatibility or performance. Use at your own risk.

Welcome to the ChainLit Chat History Persister project! This solution is designed as a custom backend compatible with ChainLit installations to enable persistent storage of chat history. Leveraging GraphQL, it aims to integrate seamlessly with the ChainLit ecosystem, providing a sturdy first step towards a customizable data layer as encouraged by the ChainLit documentation. [Custom Data Persistence in ChainLit](https://docs.chainlit.io/data-persistence/custom)


## How to Use

You can deploy this project using a Docker image from Docker Hub or by cloning the repository for a more hands-on setup. Both methods support using either a Docker-managed PostgreSQL database or an external database for flexibility.

### Running with Docker

Find a `docker-compose.yml` file in the repository for easy setup. Ensure Docker is running, and configure your environment variables based on the `env.example` file.

#### Required Environment Variables

```plaintext
DB_USER=postgres
DB_PASSWORD=admin
DB_NAME=my_db
PGADMIN_EMAIL=your_admin_email@example.com
PGADMIN_PASSWORD=admin
SECRET_KEY="qS1YEUHiwNOzndTyFDH3tBPRaircbjdo"
AWS_ACCESS_KEY_ID=AKIAYOURACCESSKEYID123
AWS_SECRET_ACCESS_KEY=YourSecretAccessKey123456789
AWS_DEFAULT_REGION=us-east-2
AWS_BUCKET_NAME=my-chat-data-bucket
LITERAL_API_KEY=jcWHbzz5H2iDh87am__kpfySr76akh72Ic2VG_FjtmA # read below info about this.
```
:exclamation:**Important Clarification Regarding API Key**: The `LITERAL_API_KEY` mentioned in the setup instructions is **not** the official API key provided by literalai. It's a unique identifier that you will use within this project. While it's technically possible to use an API key generated by the literalai website, we **strongly recommend** using a different, project-specific key for enhanced security and separation of concerns.

Ensure the `LITERAL_API_KEY` matches between your server and ChainLit app project. Otherwise you will get an error that apikey is not valid.

#### Starting the Service

Run the following command to start the Docker container:
```bash
docker compose up -d
```
For setups utilizing an external PostgreSQL database, replace `docker-compose.yml` with `docker-compose-external-db.yml` and update it with your database details.

## Project Overview

The initiative behind this project is to allow users to maintain control over their chat history, ensuring data persists across updates to the ChainLit server environment. This backend solution is compatible with ChainLit version 1.0.502, with plans to support newer versions shortly. If you require compatibility with an older version of ChainLit, please reach out so we can consider your needs.

### Key Features

- **Persistent Chat History:** Keeps your chat data safe and retrievable.
- **Compatibility:** Works with ChainLit version 1.0.502. Also there are images for Chainlit version 1.0.40, 1.0.50 in case you need it. You can find all images here: [https://hub.docker.com/repository/docker/bitacoraai/chainlit-graphql/general](https://hub.docker.com/repository/docker/bitacoraai/chainlit-graphql/general). Each image has the Chainlit version it work with as tag.
- **Flexible Storage Options:** Supports both Docker-managed PostgreSQL databases and external databases. Non-text data requires an S3 bucket for storage.

### Current Limitations

- **No UI for Observability:** In this release, there's no dedicated UI for data management or observation. Database queries are currently the method for data retrieval.
- **Initial Setup Requirements:** User and API key generation occur at the first application run; a more refined management system is planned for future releases.

### Collaboration and Feedback

We welcome contributions and feedback to improve this project. Stay tuned for more detailed instructions on how to collaborate.

### Future Plans

-   UI development for better observability and management of chat history.
-   Expanding compatibility to newer versions of ChainLit.
-   Enhancing the test suite to cover all ChainLit features.

### Acknowledgements

Our project harnesses the power of FastAPI and Strawberry GraphQL, chosen for their reliability and scalability. We acknowledge that ChainLit and literalai might utilize alternative technologies, such as Node.js and GraphQL Yoga, for their solutions. Our selection of Python and its vibrant ecosystem aims to complement these technologies, not to overshadow them. We're enthusiastic about exploring how our choice can harmoniously integrate with the diverse tech stacks used in the ChainLit and literalai ecosystems, fostering seamless compatibility and enhanced performance.

### Stay Tuned

A comprehensive tutorial will soon be available on YouTube, walking through each setup step in detail.

----------

Your feedback is crucial to us as we navigate the initial release phase. Please report any issues or suggestions to help us improve. Together, we can build a more robust and user-friendly ChainLit chat history persistence solution.
