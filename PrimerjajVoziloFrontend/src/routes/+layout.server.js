export function load({ cookies }) {
    const logged = cookies.get("logged_in");

    return {
        logged
    };
}