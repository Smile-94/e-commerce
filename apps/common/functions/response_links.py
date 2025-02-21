def get_response_links(action: str, url_prefix: str, *args, **kwargs) -> dict:
    # Use match-case for action handling
    match action:
        case "create":
            return {
                "update": f"/{url_prefix}/update/id/",
                "list": f"/{url_prefix}/list/",
                "details": f"/{url_prefix}/details/id/",
                "delete": f"/{url_prefix}/delete/id/",
            }
        case "update":
            return {
                "create": f"/{url_prefix}/create/",
                "update": f"/{url_prefix}/update/id/",
                "list": f"/{url_prefix}/list/",
                "details": f"{url_prefix}/details/id/",
                "delete": f"/{url_prefix}/delete/id/",
            }
        case "list":
            return {
                "create": f"/{url_prefix}/create/",
                "update": f"/{url_prefix}/update/id/",
                "details": f"/{url_prefix}/details/id/",
                "delete": f"/{url_prefix}/delete/id/",
            }
        case "details":
            return {
                "create": f"/{url_prefix}/create/",
                "update": f"/{url_prefix}/update/id/",
                "list": f"/{url_prefix}/list/",
                "delete": f"/{url_prefix}/delete/id/",
            }
        case "delete":
            return {
                "create": f"/{url_prefix}/create/",
                "update": f"/{url_prefix}/update/id/",
                "list": f"/{url_prefix}/list/",
                "details": f"/{url_prefix}/details/id/",
            }

        case "upload":
            return {
                "list": f"/{url_prefix}/list/",
            }
        case _:
            return {}  # Return an empty dict for unrecognized actions
