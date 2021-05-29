#!/usr/bin/bash

# remove config file if it exists
configFile=dwh.cfg
if [ -f "$configFile" ]
then
    rm "$configFile"
fi

# read in the config template file
config_template=$(<dwh_template.cfg)

# replace the placeholders in template with value from the secret files
for secret in terraform/secrets/*.txt
do
    # get the file name only
    # ref: https://stackoverflow.com/a/965072/11868112
    filename_with_extension=$(basename -- $secret)
    filename_without_extension="${filename_with_extension%.*}"
    # filename_with_extension=$(echo $secret | rev | cut -d'/' -f1 | rev)
    # filename_without_extension=$(echo $secret_name | cut -d'.' -f1)

    # capitalize the name
    secret_name=$(echo $filename_without_extension | tr a-z A-Z)

    # placeholder name to replace
    placeholder_to_replace="SECRET_$secret_name"

    # read the content from the secret file and replace the matching placeholder in the string from template file
    secret_content=$(<$secret)
    if [ $placeholder_to_replace = 'SECRET_HOST' ]
    then
        # endpoint consists of both url and port delimited by ':',i.e. url:port
        # but we only need the url
        IFS=':' read -r secret_content port <<< "$secret_content" 
    fi

    # use a different character other thean / as regexp delimiter to avoid escaping the "/" in ARN
    # here we use ,
    sed_line="s,$placeholder_to_replace,$secret_content,"
    config_template=$(echo "$config_template" | sed $sed_line)
done

# ref: https://www.oreilly.com/library/view/learning-linux-shell/9781788993197/a7ed8d81-e932-4ff8-b77f-8af922b88aad.xhtml
# assign descriptor 3 to config file to be used
exec 3> dwh.cfg

# preserve newlines by setting IFS to empty
IFS=

# write back the content of template to config file
echo $config_template >&3

# close config file
exec 3<&-