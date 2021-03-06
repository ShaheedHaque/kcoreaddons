cmake_minimum_required(VERSION 2.8.12)

project(KCoreAddons)

include(FeatureSummary)
find_package(ECM 5.22.0  NO_MODULE)
set_package_properties(ECM PROPERTIES TYPE REQUIRED DESCRIPTION "Extra CMake Modules." URL "https://projects.kde.org/projects/kdesupport/extra-cmake-modules")
feature_summary(WHAT REQUIRED_PACKAGES_NOT_FOUND FATAL_ON_MISSING_REQUIRED_PACKAGES)


set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)


include(GenerateExportHeader)
include(ECMPackageConfigHelpers)
include(ECMSetupVersion)
include(ECMGenerateHeaders)

include(KDEInstallDirs)
include(KDEFrameworkCompilerSettings NO_POLICY_SCOPE)
include(KDECMakeSettings)

set(REQUIRED_QT_VERSION 5.4.0)
find_package(Qt5 ${REQUIRED_QT_VERSION} CONFIG REQUIRED Core)

find_package(Threads)

# Configure checks for kdirwatch
find_package(FAM)

set_package_properties(FAM PROPERTIES
     PURPOSE "Provides file alteration notification facilities using a separate service. FAM provides additional support for NFS.")

set(HAVE_FAM ${FAM_FOUND})

option(ENABLE_INOTIFY "Try to use inotify for directory monitoring" ON)
if(ENABLE_INOTIFY)
    include(CheckIncludeFiles)
    check_include_files(sys/inotify.h SYS_INOTIFY_H_FOUND)
    set(HAVE_SYS_INOTIFY_H ${SYS_INOTIFY_H_FOUND})
endif()

# Generate io/config-kdirwatch.h
configure_file(src/lib/io/config-kdirwatch.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/src/lib/io/config-kdirwatch.h)

include(ECMPoQmTools)

set(KF5_VERSION "5.22.0") # handled by release scripts

ecm_setup_version(${KF5_VERSION} VARIABLE_PREFIX KCOREADDONS
                        VERSION_HEADER "${CMAKE_CURRENT_BINARY_DIR}/kcoreaddons_version.h"
                        PACKAGE_VERSION_FILE "${CMAKE_CURRENT_BINARY_DIR}/KF5CoreAddonsConfigVersion.cmake"
                        SOVERSION 5)


if (IS_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/po")
    ecm_install_po_files_as_qm(po)
endif()

kde_enable_exceptions()

add_subdirectory(src)
add_subdirectory(autotests)
add_subdirectory(tests)

# create a Config.cmake and a ConfigVersion.cmake file and install them
set(CMAKECONFIG_INSTALL_DIR "${KDE_INSTALL_CMAKEPACKAGEDIR}/KF5CoreAddons")

ecm_configure_package_config_file("${CMAKE_CURRENT_SOURCE_DIR}/KF5CoreAddonsConfig.cmake.in"
                              "${CMAKE_CURRENT_BINARY_DIR}/KF5CoreAddonsConfig.cmake"
                              INSTALL_DESTINATION  ${CMAKECONFIG_INSTALL_DIR}
                              )

install(FILES  "${CMAKE_CURRENT_BINARY_DIR}/KF5CoreAddonsConfig.cmake"
               "${CMAKE_CURRENT_BINARY_DIR}/KF5CoreAddonsConfigVersion.cmake"
               "${CMAKE_CURRENT_SOURCE_DIR}/KF5CoreAddonsMacros.cmake"
        DESTINATION "${CMAKECONFIG_INSTALL_DIR}"
        COMPONENT Devel )

install(EXPORT KF5CoreAddonsTargets DESTINATION "${CMAKECONFIG_INSTALL_DIR}" FILE KF5CoreAddonsTargets.cmake NAMESPACE KF5:: )
install(EXPORT KF5CoreAddonsToolingTargets DESTINATION "${CMAKECONFIG_INSTALL_DIR}" FILE KF5CoreAddonsToolingTargets.cmake NAMESPACE KF5:: )

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/kcoreaddons_version.h
        DESTINATION ${KDE_INSTALL_INCLUDEDIR_KF5} COMPONENT Devel )

feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)
