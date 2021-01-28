#!/bin/bash
# run as root
# places a script on path that calls the executable in this directory's dist folder
current_dir=$(pwd)
executable_dir="${current_dir}/dist/han-segmenter"
echo "#!/bin/bash" > /usr/local/bin/han-segmenter
echo "cd ${executable_dir}">> /usr/local/bin/han-segmenter
echo "./han-segmenter "'"$@"' >> /usr/local/bin/han-segmenter
chmod +x /usr/local/bin/han-segmenter

