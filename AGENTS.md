# Repository agent rules

## Git permissions and scope
- The user permits Git commands in this repository without per-command confirmation. This applies only to `/home/kris/Prog/projects/token-burner`; never infer the permission for another repository.
- Do not change global or system Git configuration. Keep any repository-specific configuration local to this repository.

## Commit policy
- Commit coherent, validated milestones, not individual file saves or one-line edits. Group related code, data, documentation, generated outputs, and state updates.
- Aim for one commit per completed stage or batch; combine small related stages when that makes a cleaner checkpoint, and split a large stage only at meaningful boundaries.
- Before committing, update persistent state, run relevant checks, and inspect status and the staged diff. Exclude secrets, throwaway files, and unrelated changes.
- Use short commit messages that describe the milestone. Do not manufacture a daily commit quota or split work just to create more versions.
