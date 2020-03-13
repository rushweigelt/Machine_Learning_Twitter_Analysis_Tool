/*
Data Management is a package for large scale interactions with the Twitter API for TAT
Its main features are:
	- Data retrieval from Twitter with arbitrary parameters
	- Pushing Data to the locally hosted Mongo DB
	- Normalizing collected data

Potential features are:
 	- Arbitrary data normalization
 */

package main

import (
	"context"
	"fmt"
	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"io/ioutil"
	"strings"

	//"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"os"
)

// TODO: Get from a config or Docker Env var, DO NOT COMMIT THIS
const CONSUMER_KEY string = "XLuTfzcgjUtlZs4dzGM3W2tq6"
const CONSUMER_SECRET string = "FfTFPxwhiI97wuy9TOe6Lq8Sgl8phJRFQNaukQbEXg6oblyuzJ"
const ACCESS_TOKEN string = "1179141952794583042-IPNL6nE2SdzZnG26p3Ld5TgpBSNfA9"
const ACCESS_SECRET string = "ptuUKpOGbUZIg8alVapQdXg3ibPdoBMwGT5LBDW4DRcgK"

const HASHTAGFILE = "Hashtags"
const USERFILE = "Users"

// TODO: Create routine for grabbing historical tweets by hashtag
// TODO: Setup and teardown code for Mongo/Twitter API calls
// TODO: Mongo Emission info
// TODO: STRETCH routine for grabbing realtime data by hashtag

func getQueryParams(queryFile string) *[]string {
	file, err := os.Open(queryFile)
	if err != nil {
		log.Fatal("No query file found")
	}
	text, err := ioutil.ReadAll(file)
	textString := string(text)
	queryList := strings.Split(textString, "\n")
	return &queryList
}

func PushTweetsToMongo(mongoClient *mongo.Client, database string, collectionName string, tweets *[]twitter.Tweet) {
	total := 0
	collection := mongoClient.Database(database).Collection(collectionName)
	for _, tweet := range *tweets {
		result, err := collection.InsertOne(context.TODO(), tweet)
		if err != nil {
			log.Fatal(err)
		}
		total += 1
		_ = result
	}
	log.Printf("Pushed %v tweets to databse %s with collection %s ", total, database, collectionName)
	return
}

func queryTwitterSearch(twitterClient *twitter.Client, queryString string) *[]twitter.Tweet {
	search, resp, err := twitterClient.Search.Tweets(&twitter.SearchTweetParams{
		Query: queryString,
		Count: 100,
		TweetMode: "extended",
	})
	if err != nil {
		log.Fatal(err)
	}
	if resp.StatusCode == 200 {
		log.Println("Got back a positive response from twitter")
		return &search.Statuses
	} else {
		log.Fatal("Bad Status Code from Twitter")
	}
	return nil
}

func queryTwitterUser(twitterClient *twitter.Client, user string) *[]twitter.Tweet {
	var userParams = twitter.UserTimelineParams{
		ScreenName: user,
		Count:      200,
		TweetMode: "extended",
	}

	returnedTimeline, resp, err := twitterClient.Timelines.UserTimeline(&userParams)
	if err != nil {
		log.Fatal(err)
	}

	if resp.StatusCode != 200 {
		log.Fatal(resp)
	}
	return &returnedTimeline
}

func main() {
	// Create and connect to our mongo instance
	// TODO: Set by config
	mongo_client_options := options.Client().ApplyURI("mongodb://localhost:27017")
	mongo_client, err := mongo.Connect(context.TODO(), mongo_client_options)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Created Client")

	err = mongo_client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("MongoDB is up, connecting to Twitter ")

	twitterConfig := oauth1.NewConfig(CONSUMER_KEY, CONSUMER_SECRET)
	twitterToken := oauth1.NewToken(ACCESS_TOKEN, ACCESS_SECRET)
	httpClient := twitterConfig.Client(oauth1.NoContext, twitterToken)

	twitterClient := twitter.NewClient(httpClient)

	// Get the hashtags we need
	hashtags := getQueryParams(HASHTAGFILE)
	users := getQueryParams(USERFILE)

	for _, hashtag := range *hashtags {
		if hashtag == "" {
			log.Println("WARN: Empty string found, breaking")
			break
		}
		log.Println("sending twitter a request for " + hashtag)
		// Pull info from twitter with query as hashtag
		PushTweetsToMongo(mongo_client, "Hashtags", hashtag, queryTwitterSearch(twitterClient, "#"+hashtag))
	}

	for _, user := range *users {
		if user == "" {
			log.Println("WARN: Empty string found")
		}
		// Grab user's tweets, push them to mongo
		PushTweetsToMongo(mongo_client, "Users", user, queryTwitterUser(twitterClient, user))
	}

}
