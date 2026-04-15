package main

import (
	"log"

	"github.com/example/reddit-wallpaper-archiver/internal/reddit"
	"github.com/example/reddit-wallpaper-archiver/internal/storage"
)

func main() {
	posts := []reddit.SavedPost{
		{ID: "a1", Subreddit: "wallpapers", URL: "https://example.com/one.jpg", Title: "Aurora"},
		{ID: "a2", Subreddit: "golang", URL: "https://example.com/two.jpg", Title: "Not wallpaper"},
	}

	filtered := reddit.FilterWallpaperPosts(posts)
	assets := make([]storage.Asset, 0, len(filtered))
	for _, post := range filtered {
		assets = append(assets, storage.Asset{
			ID:    post.ID,
			Title: post.Title,
			URL:   post.URL,
		})
	}

	if err := storage.WriteManifest("data/manifest.json", assets); err != nil {
		log.Fatal(err)
	}

	log.Printf("Archived %d wallpaper assets", len(assets))
}
