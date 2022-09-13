#!/usr/bin/env python3
#
# Copyright (C) 2022 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Manages the release process for Bazel binary.

This script walks the user through all steps required to cut a new
Bazel binary (and related artifacts) for AOSP. This script is intended
for use only by the current Bazel release manager.

Use './release_bazel.py --help` for usage details.
"""

import argparse
import sys


# Prompts the user for y/n input using the given string. Will not return until
# the user specifies either "y" or "n".
# Returns True if the user responded "y" and False if the user responded "n".
def prompt(s):
  while True:
    response = input(s + " (y/n): ")
    if response == "y":
      print()
      return True
    elif response == "n":
      print()
      return False
    else:
      print("'%s' invalid, please specify y or n." % response)


def target_update_commit(args):
  if args.commit is None:
    # TODO(b/239044269): Obtain the most recent pre-release Bazel commit
    # from github.
    raise Exception("Must specify a value for --commit")
  return args.commit


# Verify that the target commit is newer than the commit of the current
# prebuilt bazel.
def ensure_commit_is_new(commit):
  # TODO(b/239044269): Automate instead of asking the user.
  is_new_input = prompt("Is commit %s newer than the current Bazel " % commit
                        + "prebuilt's commit?")
  if not is_new_input:
    print(f"commit {commit} is not newer than the current Bazel commit. "
          + "Do not release a new Bazel.")
    sys.exit(1)


# Ensures that relevant projects in the working directory are clean, have
# new release-related branches, and synced to HEAD.
def ensure_projects_clean():
  # TODO(b/239044269): Automate instead of asking the user.
  is_new_input = prompt("Are all relevant local projects in your working "
                        + "directory clean (fresh branches) and synced to "
                        + "HEAD?")
  if not is_new_input:
    print("Please ready your local projects before continuing with the "
          + "release script")
    sys.exit(1)


# Run the update script to retrieve a prebuilt bazel at the given commit, and
# update other checked in bazel prebuilts using bazel source tree at that
# commit.
def run_update():
  print("Run the update script prebuilts/bazel/common/update.sh")
  # TODO(b/239044269): Automate instead of asking the user.
  was_update_run = prompt("Did the update script successfully run?")
  if not was_update_run:
    sys.exit(1)


# Run tests to verify the integrity of the Bazel release.
# Failure during this step will require manual intervention by the user;
# a failure might be fixed by updating other dependencies in the Android
# tree, or might indicate that Bazel at the given commit is problematic
# and the release may need to be abandoned.
def verify_update():
  print("Verify the release by running postsubmit scripts.")
  # TODO(b/239044269): Automate instead of asking the user.
  was_update_run = prompt("Have you run all verification successfully?")
  if not was_update_run:
    print("Please remedy all issues until verification runs successfully.\n"
          + "You may skip to the verify step in this script by using "
          + "--verify-only")
    sys.exit(1)


# Create commits using `repo` for all projects related to the Bazel release.
def create_commits():
  print("Create CLs for all projects that need to be updated.")
  # TODO(b/239044269): Automate instead of asking the user.
  commits_created = prompt("Have you created CLs for all projects that need "
                           + "to be updated?")
  if not commits_created:
    print("Create CLs for all projects. After approval and CL submission, the "
          + "release is complete.")
    sys.exit(1)


def main():
  parser = argparse.ArgumentParser(
      description="Walks the user through all steps required to cut a new "
      + "Bazel binary (and related artifacts) for AOSP. This script is "
      + "intended for use only by the current Bazel release manager.")
  parser.add_argument("--commit", default=None,
                      help="the bazel commit hash to use. If unspecified, " +
                      "will use the most recent prerelease Bazel")
  parser.add_argument("--verify-only", action=argparse.BooleanOptionalAction,
                      help="If true, will only do verification and CL "
                      + "creation if verification passes.")
  args = parser.parse_args()

  if not args.verify_only:
    commit = target_update_commit(args)
    ensure_commit_is_new(commit)
    ensure_projects_clean()
    run_update()

  verify_update()
  create_commits()

  print("Bazel release verified and CLs sent for approval. After approval and "
        + "CL submission, the release is complete.")


if __name__ == "__main__":
  main()
