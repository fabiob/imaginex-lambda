from operator import itemgetter
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from imaginex_lambda.handler import download_and_optimize

THIS_DIR = Path(__file__).parent

with (THIS_DIR / 'test_samples.yaml').open() as f:
    samples = yaml.safe_load(f)


@pytest.mark.parametrize(argnames := 'q,w,path', [
    tuple(get(node) for get in (itemgetter(k) for k in argnames.split(',')))
    for node in samples
])
def test_sample(q, w, path):
    with patch('imaginex_lambda.handler.S3_BUCKET_NAME', 'sladg-imaginex'):
        image_data, content_type, ratio = download_and_optimize(url=path, quality=q, width=w)
        assert isinstance(image_data, bytes)
        assert ratio < 0.5
