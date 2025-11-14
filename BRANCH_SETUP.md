# Setting backend_ai2 as Default Branch

## Overview

The `backend_ai2` branch contains the latest features and improvements for PersonaReflect, including:
- Voice input functionality
- Emotion charts
- Enhanced Google Calendar integration
- Updated README and documentation
- Additional frontend improvements

This branch should be set as the default branch for the repository.

## How to Change Default Branch in GitHub

### For Repository Owners/Admins:

1. **Navigate to Repository Settings**
   - Go to your repository on GitHub: https://github.com/yuancx2025/hackDuke2025
   - Click on "Settings" (you need admin access)

2. **Access Branch Settings**
   - In the left sidebar, click on "Branches"
   - Look for the "Default branch" section

3. **Change Default Branch**
   - Click the switch/edit icon next to the current default branch
   - Select `backend_ai2` from the dropdown menu
   - Click "Update" or "Save"
   - Confirm the change when prompted

4. **Verify the Change**
   - The default branch should now show `backend_ai2`
   - New clones will automatically checkout this branch
   - Pull requests will default to this branch as the base

## Why backend_ai2?

The `backend_ai2` branch represents the current state of development with:
- More commits and recent updates
- Additional features not present in `main`
- Better integration with the latest Google ADK features
- Improved user experience with voice and emotion tracking

## Impact

Once the default branch is changed:
- New contributors will automatically work on the latest code
- Documentation in README.md already references this branch
- No code changes are needed - this is purely a GitHub repository setting
- Existing clones on other branches are unaffected

## Alternative: Branch Protection

Consider also setting up branch protection rules for `backend_ai2`:
1. Settings → Branches → Branch protection rules
2. Add a rule for `backend_ai2`
3. Enable:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Include administrators (optional)
