FROM xsteadfastx/alpine-x86:3.4

RUN apk add --update \
      su-exec \
      redis \
 && rm -rf /var/cache/apk/*

EXPOSE 6379
CMD ["su-exec", "redis", "redis-server", "--protected-mode no"]
