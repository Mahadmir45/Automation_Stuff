# Reddit Wallpaper Archiver (Go)

A Go service that fetches saved Reddit posts, filters wallpaper sources, and archives images and metadata for Git-backed storage.

## Scope

- reads saved posts
- filters by subreddit pattern (`wallpaper`, `wallpapers`)
- drops invalid URLs and deduplicates repeated assets
- stores metadata manifest for traceability

## Run

```bash
go run ./cmd/archiver
```

Custom manifest destination:

```bash
go run ./cmd/archiver --manifest-path data/manifest.json
```
