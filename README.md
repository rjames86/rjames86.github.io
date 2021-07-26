# Docker commands

    ## Devserver

    docker run --rm -it -p 8000:8000 \
        -v $(pwd)/content:/website/content:ro \
        -v $(pwd)/output:/website/output \
        -w /website \
        --env PELICANOPTS="--bind=0.0.0.0" \
        ryanmoco \
        make devserver