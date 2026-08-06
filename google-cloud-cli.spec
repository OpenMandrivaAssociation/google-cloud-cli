# Google Cloud CLI — install the official packager SDK tree with system Python.
# Google does not publish a traditional buildable source tree for gcloud; the
# for_packagers tarball is the Python source distribution intended for distros.
# Prebuilt pieces (bundled CPython, gcloud-crc32c Go binary) are stripped.
# Overlapping pure-Python deps that OpenMandriva already packages (e.g. urllib3)
# are removed so the system copies are used.

Name:		google-cloud-cli
Version:	579.0.0
Release:	3
Summary:	Command-line tools for Google Cloud Platform
License:	Apache-2.0
Group:		Development/Other
URL:		https://cloud.google.com/cli
# Official packager archive (versioned). Arch-specific bits (bundled Python,
# gcloud-crc32c) are removed so the package is noarch.
Source0:	https://dl.google.com/dl/cloudsdk/release/downloads/for_packagers/linux/google-cloud-cli_%{version}.orig_amd64.tar.gz#/%{name}-%{version}.tar.gz
Source1:	google-cloud-cli.sh
# Consumed automatically by package check when named google-cloud-cli.rpmlintrc
Source2:	google-cloud-cli.rpmlintrc

BuildArch:	noarch
BuildRequires:	python
# %check exercises gcloud with site-packages
BuildRequires:	python%{pyver}dist(urllib3)
BuildRequires:	python%{pyver}dist(requests)
BuildRequires:	python%{pyver}dist(pyopenssl)
BuildRequires:	python%{pyver}dist(cryptography)

Requires:	python >= 3.10

# --- System Python modules replacing Google's vendored third_party ---
# HTTP / TLS stack
Requires:	python%{pyver}dist(urllib3)
Requires:	python%{pyver}dist(requests)
Requires:	python%{pyver}dist(certifi)
Requires:	python%{pyver}dist(idna)
Requires:	python%{pyver}dist(charset-normalizer)
Requires:	python%{pyver}dist(chardet)
Requires:	python%{pyver}dist(cryptography)
Requires:	python%{pyver}dist(pyopenssl)
Requires:	python%{pyver}dist(cffi)
Requires:	python%{pyver}dist(pycparser)
# AWS transfer path (gcloud transfer / storage extras → boto3)
Requires:	python%{pyver}dist(botocore)
Requires:	python%{pyver}dist(boto3)
Requires:	python%{pyver}dist(s3transfer)
Requires:	python%{pyver}dist(jmespath)
# Auth / OAuth (top-level modules; google.auth itself stays in vendored google/)
Requires:	python%{pyver}dist(google-auth)
Requires:	python%{pyver}dist(google-auth-oauthlib)
Requires:	python%{pyver}dist(google-auth-httplib2)
Requires:	python%{pyver}dist(requests-oauthlib)
Requires:	python%{pyver}dist(oauthlib)
Requires:	python%{pyver}dist(oauth2client)
Requires:	python%{pyver}dist(rsa)
Requires:	python%{pyver}dist(pyasn1)
Requires:	python%{pyver}dist(pyasn1-modules)
Requires:	python%{pyver}dist(httplib2)
Requires:	python%{pyver}dist(uritemplate)
Requires:	python%{pyver}dist(google-api-python-client)
# Common libraries
Requires:	python%{pyver}dist(argcomplete)
Requires:	python%{pyver}dist(attrs)
Requires:	python%{pyver}dist(cachetools)
Requires:	python%{pyver}dist(python-dateutil)
Requires:	python%{pyver}dist(dnspython)
Requires:	python%{pyver}dist(python-dotenv)
Requires:	python%{pyver}dist(dulwich)
Requires:	python%{pyver}dist(jsonschema)
Requires:	python%{pyver}dist(mako)
Requires:	python%{pyver}dist(markupsafe)
Requires:	python%{pyver}dist(packaging)
Requires:	python%{pyver}dist(prompt-toolkit)
Requires:	python%{pyver}dist(pygments)
Requires:	python%{pyver}dist(pyparsing)
Requires:	python%{pyver}dist(pytz)
Requires:	python%{pyver}dist(six)
Requires:	python%{pyver}dist(wcwidth)
Requires:	python%{pyver}dist(websocket-client)
Requires:	python%{pyver}dist(pyyaml)
# ruamel stays vendored: system ruamel.yaml dropped the yaml.load() API gcloud uses
Requires:	python%{pyver}dist(fasteners)
Requires:	python%{pyver}dist(cattrs)
Requires:	python%{pyver}dist(docker)
Requires:	python%{pyver}dist(sqlparse)
Requires:	python%{pyver}dist(crcmod)
Requires:	python%{pyver}dist(monotonic)
Requires:	python%{pyver}dist(protobuf)
Requires:	python%{pyver}dist(tabulate)
Requires:	python%{pyver}dist(ply)
Requires:	python%{pyver}dist(appdirs)
Requires:	python%{pyver}dist(termcolor)
Requires:	python%{pyver}dist(typing-extensions)
Requires:	python%{pyver}dist(wrapt)
Requires:	python%{pyver}dist(mock)

Provides:	google-cloud-sdk = %{EVRD}
Provides:	gcloud = %{EVRD}
Obsoletes:	google-cloud-sdk < %{version}

%description
The Google Cloud CLI (gcloud) is a set of tools to create and manage
Google Cloud resources. This package installs gcloud core (including
alpha/beta surfaces), gsutil, bq, and credential helpers.

It uses the system Python interpreter and system Python modules instead
of Google's bundled CPython and overlapping vendored copies (security
updates via the distribution). The self-updater is disabled so updates
come from the package manager.

Google-specific trees (e.g. lib/third_party/google, cloudsdk, apitools)
that have no safe system replacement are left vendored.

Note: gcloud is distributed by Google as a Python tree rather than a
traditional rebuildable source project; this package installs that tree
and does not repackage Google's binary RPM/DEB.

%prep
%autosetup -n google-cloud-sdk

# Drop prebuilt / non-FHS pieces
rm -rf platform/bundledpythonunix
rm -f bin/gcloud-crc32c
rm -f .install/bundled-python3-unix* .install/gcloud-crc32c*
rm -f .install/*-linux-*
rm -rf deb rpm
rm -f install.bat install.sh

# ---------------------------------------------------------------------------
# Devendor: remove every third_party tree that OpenMandriva ships as a system
# package (or that is pure stdlib). gcloud puts third_party first on sys.path,
# so removal is required for system modules to be used.
#
# KEEP (no safe system replacement / gcloud-private):
#   google/  cloudsdk/  antlr3  apitools  containerregistry  fancy_urllib
#   gae_ext_runtime  gcloud_crcmod  ml_sdk  orchestration_pipelines_models
#   pubsublite  pyu2f  grpc_status  hcl2  kubernetes  lark  overrides  portpicker
#   frozendict  contextlib2  socks  win_inet_pton  functools32  backports
#   ipaddr  proto  gcs-oauth2-boto-plugin  google-reauth*  retry-decorator
#   gflags  absl  and similar Google-only or unpackaged trees
# ---------------------------------------------------------------------------
unvendor() {
	# $1 = root (e.g. lib/third_party); remaining args = dir names
	local root=$1
	shift
	local d
	[ -d "$root" ] || return 0
	for d in "$@"; do
		rm -rf "${root}/${d}"
	done
}

# Names shared across lib/, gsutil/, and bq/ third_party layouts
_common_unvendor="
	argcomplete attr attrs
	cachetools
	dateutil dns dotenv dulwich
	jsonschema
	mako markupsafe
	packaging
	prompt_toolkit
	pyasn1 pyasn1_modules pyasn1-modules
	pygments pyparsing pytz
	six
	wcwidth websocket
	yaml
	boto3 botocore s3transfer jmespath
	httplib2
	rsa
	google_auth_oauthlib
	requests_oauthlib
	docker
	sqlparse uritemplate
	fasteners
	cattr cattrs
	oauth2client oauthlib
	monotonic
	crcmod crcmod_osx
	urllib3 requests certifi idna charset_normalizer chardet
	cryptography cffi pycparser
	protobuf
	tabulate
	ply appdirs termcolor
	typing_extensions
	wrapt
	mock
	argparse concurrent ipaddress
	openssl
"

unvendor lib/third_party ${_common_unvendor}

unvendor platform/gsutil/third_party ${_common_unvendor} \
	google-auth-library-python \
	google-auth-library-python-httplib2 \
	funcsigs

unvendor platform/bq/third_party ${_common_unvendor} \
	googleapiclient \
	google_auth_httplib2 \
	oauth2client_4_0 \
	pkg_resources \
	tz

# Package manager owns updates
python - <<'PY'
import json
from pathlib import Path
p = Path("lib/googlecloudsdk/core/config.json")
data = json.loads(p.read_text())
data["disable_updater"] = True
p.write_text(json.dumps(data, indent=2) + "\n")
PY

# Ensure component snapshots do not hard-require stripped components
python - <<'PY'
import json, glob
for path in glob.glob(".install/*.snapshot.json"):
	with open(path) as f:
		try:
			data = json.load(f)
		except Exception:
			continue
	def scrub(obj):
		if isinstance(obj, dict):
			return {
				k: scrub(v)
				for k, v in obj.items()
				if "bundled-python" not in str(k) and "gcloud-crc32c" not in str(k)
			}
		if isinstance(obj, list):
			return [
				scrub(x)
				for x in obj
				if not (isinstance(x, str) and ("bundled-python" in x or "gcloud-crc32c" in x))
			]
		return obj
	scrubbed = scrub(data)
	with open(path, "w") as f:
		json.dump(scrubbed, f)
PY

# Default properties: no update check
if [ -f properties ]; then
	printf '\n[component_manager]\ndisable_update_check = true\n' >> properties
else
	printf '[component_manager]\ndisable_update_check = true\n' > properties
fi

# Remove caches
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name '*.pyc' -delete 2>/dev/null || true

%build
# Skip bulk compileall — tree still contains py2-only leftovers that are not
# imported at runtime; first-run bytecode is fine for a noarch tool package.

%install
sdkroot=%{buildroot}%{_datadir}/google-cloud-sdk
install -d -m 0755 "${sdkroot}"
cp -a . "${sdkroot}/"

# Prefer fixed interpreter paths (rpmlint env-script-interpreter).
# Only rewrite files that actually use env shebangs (few compared to whole tree).
grep -rlZ --include='*.py' --include='gsutil' --include='bq' --include='gcloud' \
	'^#!/usr/bin/env python' "${sdkroot}" \
	| xargs -0 -r sed -i \
		-e '1s|^#! */usr/bin/env python3\>|#!/usr/bin/python|' \
		-e '1s|^#! */usr/bin/env python\>.*|#!/usr/bin/python|' \
	|| true

install -d -m 0755 %{buildroot}%{_sysconfdir}/profile.d
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/google-cloud-cli.sh

# Relative command symlinks — gcloud resolves ROOT via realpath of the script
install -d -m 0755 %{buildroot}%{_bindir}
for cmd in gcloud bq gsutil docker-credential-gcloud git-credential-gcloud.sh; do
	ln -s ../share/google-cloud-sdk/bin/${cmd} %{buildroot}%{_bindir}/${cmd}
done

# Shell completions
install -d -m 0755 %{buildroot}%{_datadir}/bash-completion/completions
if [ -f %{buildroot}%{_datadir}/google-cloud-sdk/completion.bash.inc ]; then
	install -p -m 0644 %{buildroot}%{_datadir}/google-cloud-sdk/completion.bash.inc \
		%{buildroot}%{_datadir}/bash-completion/completions/gcloud
	ln -s gcloud %{buildroot}%{_datadir}/bash-completion/completions/gsutil
fi
install -d -m 0755 %{buildroot}%{_datadir}/zsh/site-functions
if [ -f %{buildroot}%{_datadir}/google-cloud-sdk/completion.zsh.inc ]; then
	install -p -m 0644 %{buildroot}%{_datadir}/google-cloud-sdk/completion.zsh.inc \
		%{buildroot}%{_datadir}/zsh/site-functions/_gcloud
	sed -i '1i#compdef gcloud' %{buildroot}%{_datadir}/zsh/site-functions/_gcloud
fi

# Fail if any Linux ELF slipped in (noarch package)
elf_hits=
while IFS= read -r -d '' f; do
	case "$(head -c 4 "$f" 2>/dev/null | od -An -tx1)" in
	*7f\ 45\ 4c\ 46*) elf_hits="$elf_hits$f\n" ;;
	esac
done < <(find %{buildroot}%{_datadir}/google-cloud-sdk -type f \( -name '*.so' -o -name '*.so.*' -o -name 'gcloud-crc32c' \) -print0 2>/dev/null || true)
if [ -n "$elf_hits" ]; then
	echo "ERROR: Linux ELF objects remain in noarch package:" >&2
	printf '%b' "$elf_hits" >&2
	exit 1
fi

%check
export CLOUDSDK_PYTHON=%{_bindir}/python
export CLOUDSDK_PYTHON_SITEPACKAGES=1
export CLOUDSDK_CORE_DISABLE_USAGE_REPORTING=true
export HOME=$(mktemp -d)
export PATH=%{buildroot}%{_bindir}:$PATH
gcloud version
gcloud storage --help >/dev/null
# Exercises site-packages + system urllib3 (pyOpenSSL path)
gcloud transfer jobs create --help >/dev/null

%files
%license LICENSE
%doc README RELEASE_NOTES VERSION
%config(noreplace) %{_sysconfdir}/profile.d/google-cloud-cli.sh
%{_bindir}/gcloud
%{_bindir}/bq
%{_bindir}/gsutil
%{_bindir}/docker-credential-gcloud
%{_bindir}/git-credential-gcloud.sh
%{_datadir}/google-cloud-sdk/
%{_datadir}/bash-completion/completions/gcloud
%{_datadir}/bash-completion/completions/gsutil
%{_datadir}/zsh/site-functions/_gcloud
