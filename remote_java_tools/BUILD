package(default_visibility = ["//visibility:public"])

filegroup(
    name = "GenClass",
    srcs = ["java_tools/GenClass_deploy.jar"],
)

filegroup(
    name = "jacoco_coverage_runner_filegroup",
    srcs = ["java_tools/JacocoCoverage_jarjar_deploy.jar"],
)

filegroup(
    name = "JacocoCoverage",
    srcs = ["java_tools/JacocoCoverage_jarjar_deploy.jar"],
)

filegroup(
    name = "JavaBuilder",
    srcs = ["java_tools/JavaBuilder_deploy.jar"],
)

filegroup(
    name = "Runner",
    srcs = ["java_tools/Runner_deploy.jar"],
)

filegroup(
    name = "VanillaJavaBuilder",
    srcs = ["java_tools/VanillaJavaBuilder_deploy.jar"],
)

filegroup(
    name = "TurbineDirect",
    srcs = ["java_tools/turbine_direct_binary_deploy.jar"],
)

################### Proguard ###################
java_import(
    name = "proguard_import",
    jars = ["java_tools/proguard.jar"],
)

java_binary(
    name = "proguard",
    main_class = "proguard.ProGuard",
    visibility = ["//visibility:public"],
    runtime_deps = [":proguard_import"],
)
