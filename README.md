# Fastify

 Yet another Fast API CRUD Generator with some opinions.

# Dependencies

   1. [pdm](https://pdm-project.org/en/stable/) - For package manager.
   2. [textblob](https://textblob.readthedocs.io/en/dev/) - For NLP module.
   3. [fastapi](https://fastapi.tiangolo.com/)  - For testing.

# Setup

1.  Clone repository
2.  Change to fastifiy root directory
3.  Run pdm dependencies
   `pdm install`
4.  Activate virtual environment
   `eval $(pdm venv activate)`
5. Download textblob corpora
   ```
   # pdm add textblob
   # python -m textblob.download_corpora
   ```
6. Add sql model
   `pdm add sqlmodel`

### Usage
From fastify root directy run this command
`./fastify <model-name> <you-app-api-dir>`

1. <b>model-name</b> : Singular form of model to create (e.g. For class model 'Companies' model-name = 'company'. The script will handle the conversion to plural.)

2. <b>app-root-dir</b> : The root folder of the app. (eg. My-IoT-Device-API  or .)