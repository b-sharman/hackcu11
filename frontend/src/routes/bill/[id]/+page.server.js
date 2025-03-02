import { error } from "@sveltejs/kit";

export function load({ params }) {
    const bill_id = params.id;

    return {
        bill_id
    };
}
