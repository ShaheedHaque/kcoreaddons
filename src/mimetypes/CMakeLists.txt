# always install the mime-types
install(FILES kde5.xml DESTINATION ${KDE_INSTALL_MIMEDIR})

# for KDE frameworks 5 we require at least version 0.70
find_package(SharedMimeInfo 0.70)
set_package_properties(SharedMimeInfo PROPERTIES
                       TYPE OPTIONAL
                       PURPOSE "Allows KDE applications to determine file types"
                      )

# update XDG mime-types if shared mime info is around
if(SharedMimeInfo_FOUND)
    update_xdg_mimetypes(${KDE_INSTALL_MIMEDIR})
endif()
