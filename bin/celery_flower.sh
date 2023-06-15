#!/bin/bash
exec celery flower --app wagtailblog --workdir src
