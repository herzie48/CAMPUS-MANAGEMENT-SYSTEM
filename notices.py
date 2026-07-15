import utils
import file_manager

def add_notice(data):
    """Publishes a new notice to the notice board."""
    utils.print_header("Add New Notice")
    notices = data["notices"]
    
    # Generate sequential notice ID
    existing_ids = [int(nid[1:]) for nid in notices.keys() if nid.startswith("N") and nid[1:].isdigit()]
    next_id = 1 if not existing_ids else max(existing_ids) + 1
    nid = f"N{next_id}"
    
    title = utils.get_valid_string("Enter Notice Title: ")
    content = utils.get_valid_string("Enter Notice Content: ")
    date_str = utils.get_current_datetime().split(" ")[0]  # Just YYYY-MM-DD
    
    notices[nid] = {
        "notice_id": nid,
        "date": date_str,
        "title": title,
        "content": content
    }
    file_manager.save_notices(notices)
    utils.print_success("Notice posted successfully.")

def delete_notice(data):
    """Deletes an announcement from the board by notice ID."""
    utils.print_header("Delete Notice")
    notices = data["notices"]
    
    if not notices:
        utils.print_info("No notices available to delete.")
        return
        
    nid = utils.get_valid_string("Enter Notice ID to delete (e.g. N1): ").upper()
    if nid not in notices:
        utils.print_error("Notice ID not found.")
        return
        
    confirm = input(f"Are you sure you want to delete Notice '{notices[nid]['title']}'? (Y/N): ").strip().upper()
    if confirm == "Y":
        del notices[nid]
        file_manager.save_notices(notices)
        utils.print_success("Notice removed.")
    else:
        utils.print_info("Deletion cancelled.")

def view_notices(data):
    """Renders all active announcements posted on the notice board."""
    utils.print_header("Campus Notice Board")
    notices = data["notices"]
    
    if not notices:
        utils.print_info("No announcements posted currently.")
        return
        
    # Sort notices by ID descending (usually newer first)
    sorted_notices = sorted(notices.values(), key=lambda x: x["notice_id"], reverse=True)
    
    for note in sorted_notices:
        width = 60
        print(f"{utils.COLOR_CYAN}╔{'═' * (width - 2)}╗")
        print(f"║ {utils.COLOR_BOLD}{note['title'].ljust(width - 4)}{utils.COLOR_RESET}{utils.COLOR_CYAN} ║")
        print(f"║ Date: {note['date'].ljust(width - 10)} ID: {note['notice_id'].ljust(4)} ║")
        print(f"╠{'═' * (width - 2)}╣")
        
        # Word wrap content to fit box width
        content = note["content"]
        words = content.split(" ")
        line = ""
        for word in words:
            if len(line) + len(word) + 1 < (width - 4):
                line += word + " "
            else:
                print(f"║ {line.ljust(width - 4)} ║")
                line = word + " "
        if line:
            print(f"║ {line.ljust(width - 4)} ║")
            
        print(f"╚{'═' * (width - 2)}╝{utils.COLOR_RESET}\n")

def notice_board_menu(data, role):
    """Menu interface for Notice Board. Restricts authoring actions to admin/faculty."""
    while True:
        utils.clear_screen()
        
        if role in ["admin", "faculty"]:
            options = [
                "1. Add Notice",
                "2. Delete Notice",
                "3. View Notice Board",
                "4. Back to Main Menu"
            ]
            utils.print_box_menu("Notice Board Control Panel", options)
            choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4"])
            
            if choice == "1":
                add_notice(data)
                utils.pause()
            elif choice == "2":
                delete_notice(data)
                utils.pause()
            elif choice == "3":
                view_notices(data)
                utils.pause()
            elif choice == "4":
                break
        else:
            # Student view only
            options = [
                "1. View Notice Board",
                "2. Back to Main Menu"
            ]
            utils.print_box_menu("Student Notice Board", options)
            choice = utils.get_valid_choice("Choose option: ", ["1", "2"])
            
            if choice == "1":
                view_notices(data)
                utils.pause()
            elif choice == "2":
                break
