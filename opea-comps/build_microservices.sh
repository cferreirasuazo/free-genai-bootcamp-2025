#!/bin/bash

git clone https://github.com/opea-project/GenAIComps.git
cd GenAIComps

# Buid BEmbedding TEI Image
docker build -t opea/embedding:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f comps/embeddings/src/Dockerfile .

#Build Retriever Vector store Image
docker build -t opea/retriever:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f comps/retrievers/src/Dockerfile .

#Build Rerank TEI Image 
docker build -t opea/reranking:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f comps/rerankings/src/Dockerfile .

# Build Dataprep Image
docker build -t opea/dataprep:latest  --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f comps/dataprep/src/Dockerfile .

