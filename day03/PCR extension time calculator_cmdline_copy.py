import argparse

# Calculate the extension time for PCR reaction based on the enzyme rate and product length.
def calculate_extension_time(rate, length):
    try:
        # Calculate extension time
        extension_time = length / rate
        
        # Convert to minutes and seconds
        minutes = int(extension_time // 60)
        seconds = extension_time % 60
        
        # Print results
        print("\nResults:")
        print(f"Extension time: {extension_time:.2f} seconds")
        if minutes > 0:
            print(f"Or: {minutes} minutes and {seconds:.2f} seconds")
            
    except ZeroDivisionError:
        print("Error: Enzyme rate cannot be zero")
        return

def main():
    parser = argparse.ArgumentParser(description='Calculate PCR extension time')
    parser.add_argument('rate', type=float, help='Enzyme rate (base pairs per second)')
    parser.add_argument('length', type=float, help='PCR product length (base pairs)')
    
    args = parser.parse_args()
    calculate_extension_time(args.rate, args.length)

if __name__ == "__main__":
    main()

