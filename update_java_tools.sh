#!/bin/bash
# Updater script for Bazel java_tools prebuilt jars and binaries in AOSP.
#
# Usage: update_java_tools.sh <commit> <absolute path to prebuilts/bazel/common> <absolute path to prebuilts/bazel/linux-x86_64>

set -euo pipefail

function err() {
    >&2 echo "$@"
    exit 1
}

# Check that the necessary tools are installed.
function check_prereqs() {
    for cmd in curl xmllint git bazel-real; do
        if ! command -v "${cmd}" &> /dev/null; then
            err "Error: This script requires ${cmd}. Install it and ensure it is on your PATH."
        fi
    done
}

function check_sha256() {
  local sha256=$1; shift
  local downloaded_file=$1; shift
    echo "Verifying checksum for ${downloaded_file} to be ${sha256}.."
    if ! echo "${sha256} ${downloaded_file}" | sha256sum --check --status ; then
      echo "ERROR: checksum of ${downloaded_file} did not match!"
      echo "${sha256} ${downloaded_file}" | sha256sum --check --status
      echo "${sha256} ${downloaded_file}" | sha256sum --check
      exit 1
    fi
}

check_prereqs
commit="$1"; shift
common_bazel_dir="$1"; shift
linux_bazel_dir="$1"; shift
echo "checking out bazel..."
cd $(mktemp -d)
git clone https://github.com/bazelbuild/bazel.git
cd bazel
git checkout ${commit}
echo "gathering external repository data..."
/usr/bin/bazel-real build src:bazel_nojdk
./bazel-bin/src/bazel_nojdk query "//external:remote_java_tools + //external:remote_java_tools_linux" --output=xml > repo_infos.xml
remote_java_tools_url=$(xmllint --xpath "/query/rule[@name='//external:remote_java_tools']/list[@name='urls']/string[1]/@value" repo_infos.xml|sed -e "s/ value=\"//"|sed -e "s/\"//")
remote_java_tools_sha256=$(xmllint --xpath "/query/rule[@name='//external:remote_java_tools']/string[@name='sha256']/@value" repo_infos.xml|sed -e "s/ value=\"//"|sed -e "s/\"//")
remote_java_tools_linux_url=$(xmllint --xpath "/query/rule[@name='//external:remote_java_tools_linux']/list[@name='urls']/string[1]/@value" repo_infos.xml|sed -e "s/ value=\"//"|sed -e "s/\"//")
remote_java_tools_linux_sha256=$(xmllint --xpath "/query/rule[@name='//external:remote_java_tools_linux']/string[@name='sha256']/@value" repo_infos.xml|sed -e "s/ value=\"//"|sed -e "s/\"//")

echo "downloading remote_java_tools..."
curl "${remote_java_tools_url}" --output java_tools.zip
check_sha256 "${remote_java_tools_sha256}" "java_tools.zip"
common_jars=("JavaBuilder_deploy.jar" "turbine_direct_binary_deploy.jar" "VanillaJavaBuilder_deploy.jar" "JacocoCoverage_jarjar_deploy.jar" "GenClass_deploy.jar" "Runner_deploy.jar")
for jar in "${common_jars[@]}"
do
  unzip -o -d ${common_bazel_dir}/remote_java_tools java_tools.zip "java_tools/${jar}"
done

echo "downloading remote_java_tools_linux..."
curl "${remote_java_tools_linux_url}" --output java_tools_prebuilt.zip
check_sha256 "${remote_java_tools_linux_sha256}" "java_tools_prebuilt.zip"
common_bins=("src/tools/singlejar/singlejar_local" "ijar/ijar")
for bin in "${common_bins[@]}"
do
  unzip -o -d ${linux_bazel_dir}/remote_java_tools_linux java_tools_prebuilt.zip "java_tools/${bin}"
done
