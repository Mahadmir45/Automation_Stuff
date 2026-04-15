# Reddit Wallpaper Archiver (Go)

A Go service that fetches saved Reddit posts, filters wallpaper sources, and archives images and metadata for Git-backed storage.

## Scope

- reads saved posts
- filters by subreddit pattern (`wallpaper`, `wallpapers`)
- deduplicates by content hash
- stores metadata manifest for traceability

## Run

```bash
go run ./cmd/archiver
```
