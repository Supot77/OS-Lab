# page_table_sim.py

# System Constants
PAGE_SIZE = 1000  # In a real OS, this is usually 4096 Bytes (4KB)

# The OS Page Table: Maps [Page Number] -> [Physical Frame Number]
# Because RAM is fragmented, frames are not strictly in order!
os_page_table = {
    0: 12,  # Page 0 is stored in Frame 12
    1: 45,  # Page 1 is stored in Frame 45
    2: 8,   # Page 2 is stored in Frame 8
    3: 102, # Page 3 is stored in Frame 102
    4: 15,  # Page 4 is stored in Frame 15
    5: 33   # Page 5 is stored in Frame 33
}

def translate_address(logical_address):
    """Simulates the OS Memory Management Unit (MMU)"""
    print(f"\n[MMU] Requesting Logical Address: {logical_address}")

    # 1. Calculate Page Number and Offset
    page_number = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE
    print(f"      -> Computed Page Number: {page_number}")
    print(f"      -> Computed Offset: {offset}")

    # 2. Page Table Lookup
    if page_number not in os_page_table:
        print("      -> [OS ERROR] Page Fault! Data not in RAM (Segmentation Fault).")
        return None

    frame_number = os_page_table[page_number]
    print(f"      -> Page Table Lookup: Found in Frame {frame_number}")

    # 3. Compute Final Physical Address
    physical_address = (frame_number * PAGE_SIZE) + offset
    print(f"      -> [SUCCESS] Translated Physical Address: {physical_address}")
    return physical_address

def main():
    print("--- AI Model Address Translation Simulator ---")

    # Scenario A: Fetching the weight of Neuron at index 250
    translate_address(250)

    # Scenario B: Fetching the weight of Neuron at index 3450
    translate_address(3450)

    # Scenario C: Trying to access an index out of bounds
    translate_address(9999)

if __name__ == "__main__":
    main()
