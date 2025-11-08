def calculate_extension_time():
    print("PCR Extension Time Calculator")
    print("-" * 30)
    
    try:
        # Get user input
        rate = float(input("Enter the enzyme rate (base pairs per second): "))
        length = float(input("Enter the PCR product length (base pairs): "))
        
        # Calculate extension time
        extension_time = length / rate
        
        # Convert to minutes and seconds for better readability
        minutes = int(extension_time // 60)
        seconds = extension_time % 60
        
        # Print results
        print("\nResults:")
        print(f"Extension time: {extension_time:.2f} seconds")
        if minutes > 0:
            print(f"Or: {minutes} minutes and {seconds:.2f} seconds")
            
    except ValueError:
        print("Error: Please enter valid numbers only")
        return
    except ZeroDivisionError:
        print("Error: Enzyme rate cannot be zero")
        return

if __name__ == "__main__":
    calculate_extension_time()
    input("\nPress Enter to exit")