import argparse
from nftgen import NFTGenerator


generator = argparse.ArgumentParser(prog='generate', usage='generate.py [options]')

generator.add_argument('-n', '--amount', help="Amount to generate")
generator.add_argument('-c', '--config', help="Path to configuration file")


args = generator.parse_args()

if args.amount and args.config:
    nftgen=NFTGenerator(amount=int(args.amount))  
    nftgen.load_config_from_file(args.config)  
    nftgen.start_generating()
else:
  print('generator: error: Missing a mandatory option (-n or -c). Use -h to show the help menu.\n')

