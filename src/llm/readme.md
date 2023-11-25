# Instructions

## Setup

You will need to install the ollama package:

``` bash
curl https://ollama.ai/install.sh | sh
```

You will also need to give the script permission to run:

``` bash
chmod -R o+rx .
```

After that, you can run the following command to create the model:

``` bash
ollama create joseentregas -f Modelfile
```

## Usage

You can use the model by running the following command:

``` bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "joseentregas",
  "prompt":"ensira sua pergunta aqui",
  "stream": false
}'
```
