#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright 2023 Tatsuro Sakaguchi
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pathlib
import shutil
import subprocess

from colcon_lint.verb.lint_depends import LintVerb


def test_cmake() -> None:
    linter = LintVerb()

    tmp_dir = pathlib.Path('/tmp/colcon-lint')
    tmp_dir.mkdir(exist_ok=True)
    subprocess.Popen(['cmake',
                      '-Wno-dev',
                      '--trace-expand',
                      '--trace-redirect=trace.log',
                      pathlib.Path(__file__).parent],
                     cwd=tmp_dir,
                     stdout=subprocess.PIPE,
                     stderr=None).wait()
    trace_file = tmp_dir / 'trace.log'
    with open(trace_file) as f:
        trace_log = f.readlines()
    shutil.rmtree(tmp_dir)
    deps = linter.resolve_cmake_depends(trace_log)
    assert deps == (set(['geometry_msgs', 'rclcpp', 'std_msgs']),
                    set(['rclcpp', 'std_msgs']),
                    set(['ament_cmake']),
                    set(['ament_lint_auto']))
