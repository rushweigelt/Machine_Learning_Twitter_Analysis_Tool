package data_management

import (
	"context"
	"fmt"
	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"os"
)

// TODO: Get from a config or Docker Env var
const CONSUMER_KEY string = ""
const CONSUMER_SECRET string = ""
const ACCESS_TOKEN string = ""
const ACCESS_SECRET string = ""

const HASHTAGFILE = "Hashtags.txt"

// TODO: Create routine for grabbing historical tweets by hashtag
// TODO: Setup and teardown code for Mongo/Twitter API calls
// TODO: Mongo Emission info

// TODO: STRETCH routine for grabbing realtime data by hashtag

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

	twitter_config := oauth1.NewConfig(CONSUMER_KEY, CONSUMER_SECRET)
	twitter_token := oauth1.NewToken(ACCESS_TOKEN, ACCESS_SECRET)
	http_client := twitter_config.Client(oauth1.NoContext, twitter_token)

	twitter_client := twitter.NewClient(http_client)

	// Get the hashtags we need
	hashtags := getHashtags()
	for _, hashtag := range hashtags {
		// Pull info from twitter with query as hashtag
		// If successful
		// Create hashtag collection if it doesn't exist
		collection := mongo_client.Database("Hashtags").Collection(hashtag)
	}
}

func getHashtags() {
	file, err := os.Open(HASHTAGFILE)
    if err != nil{
    	fmt.Println("ERROR")
    	fmt.Println(err)
    }

    text, err := ioutil.ReadAll(file)
    textString := string(text)
  	hashtagList := strings.Split(textString,"\n")
  	var hashtagList2 []string

  	for _, element := range hashtagList{
  		if element[0] == 35{
  			hashtagList2 = append(hashtagList2, element[1:])
  		} else{
  			hashtagList2 = append(hashtagList2, element)
  		}
  	}
  	for _, element := range hashtagList2{
  		fmt.Println(element)
  	}
  	
	return hashtagList2
}
