package main

import (
	"flag"
	"log"

	"github.com/example/reddit-wallpaper-archiver/internal/reddit"
	"github.com/example/reddit-wallpaper-archiver/internal/storage"
)

func main() {
	manifestPath := flag.String("manifest-path", "data/manifest.json", "output path for JSON manifest")
	flag.Parse()

	posts := []reddit.SavedPost{
		{ID: "a1", Subreddit: "wallpapers", URL: "https://example.com/one.jpg", Title: "Aurora"},
		{ID: "a2", Subreddit: "golang", URL: "https://example.com/two.jpg", Title: "Not wallpaper"},
		{ID: "a3", Subreddit: "wallpaper", URL: "https://example.com/one.jpg", Title: "Duplicate"},
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

	if err := storage.WriteManifest(*manifestPath, assets); err != nil {
		log.Fatal(err)
	}

	log.Printf("Archived %d wallpaper assets to %s", len(assets), *manifestPath)
}
