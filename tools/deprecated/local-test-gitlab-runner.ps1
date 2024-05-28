#####################################################
# Locally test gitlab-runner to emulate a local build
# See ../gitlab-ci.yml
#####################################################
gitlab-runner exec shell build_latest

# Wait for user input before closing
Read-Host -Prompt "Press Enter to exit"
