# Google Cloud CLI environment (OpenMandriva package)
export CLOUDSDK_ROOT_DIR=/usr/share/google-cloud-sdk
export GOOGLE_CLOUD_SDK_HOME=$CLOUDSDK_ROOT_DIR

# System interpreter + site-packages (urllib3, requests, …). Vendored
# duplicates of those modules are stripped from the package.
if [ -z "${CLOUDSDK_PYTHON:-}" ]; then
	export CLOUDSDK_PYTHON=/usr/bin/python
fi
export CLOUDSDK_PYTHON_SITEPACKAGES=1
