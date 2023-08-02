import argparse
import layman_summaries

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Generate layman summaries from scientific abstracts")

    # Add the arguments
    parser.add_argument('--data_url', type=str, help='The URL to fetch the data from')
    parser.add_argument('--aimodel', type=str, help='The AI model to use for generation')
    parser.add_argument('--max_tokens', type=int, help='The maximum number of tokens for the generation')

    # Parse the arguments
    args = parser.parse_args()

    # Load the config.yaml file
    config = layman_summaries.load_config()

    # If data_url was provided, update the configuration
    if args.data_url is not None:
        config['data_url'] = args.data_url

    # If aimodel was provided, update the configuration
    if args.aimodel is not None:
        config['aimodel'] = args.aimodel

    # If max_tokens was provided, update the configuration
    if args.max_tokens is not None:
        config['max_tokens'] = args.max_tokens

    # Run the main function in layman_summaries.py and get the DataFrame
    df = layman_summaries.main(config)

    # Print the first 10 rows of the DataFrame
    print(df.head(10))
