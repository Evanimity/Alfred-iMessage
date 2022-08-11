# Alfred-iMessage

## Introduction
Get Verification / 2FA code from iMessage

## Requirement
- Python3 (Normally pre-installed on Mac. If not, please use `brew` to reinstall)

## Usage

### Keyword
- Open Alfred bar.
- Type `msg` in alfred.
- `Enter` to copy to clipboard, and directly paste into active textfield

### Hotkey
- `Control` + `Shift` + `m`
- `Enter` to copy to clipboard, and directly paste into active textfield

### Filter Argument
- `msg tfoo` (`foo` as integer): Filter by time, from `foo` days before, to now.
- `msg sfoo` (`foo` as any): Filter by content that contains `foo`.
- `msg ffoo` (`foo` as any): Filter by sender that contains `foo`.
- `msg lfoo` (`foo` as integer): Filter by length of code larger than `foo`.

## Config
### Config File
Config File is located at `Source/conf.json`. You may put codes (as `string` type) in 'IGNORE' to deliberately ignore those from parsing.
```json
{
    "IGNORE": [
        "10086"
    ]
}
```
