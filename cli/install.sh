#!/bin/bash
# run as root
# places a script on path that calls the executable in this directory's dist folder
current_dir=$(pwd)
executable_path="${current_dir}/dist/han-segmenter/han-segmenter"
echo "#!/bin/bash" > /usr/local/bin/han-segmenter
echo "${executable_path} "'"$@"' >> /usr/local/bin/han-segmenter
chmod +x /usr/local/bin/han-segmenter

