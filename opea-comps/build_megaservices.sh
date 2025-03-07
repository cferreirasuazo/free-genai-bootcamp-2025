git clone https://github.com/opea-project/GenAIExamples.git
cd GenAIExamples/DocIndexRetriever
docker build --no-cache -t opea/doc-index-retriever:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f ./Dockerfile .