from popconn.stats.metrics import (  # noqa: F401
    correlation_matrix_difference,
    degree_difference,
    frobenius_norm_difference,
    global_efficiency_difference,
    strength_difference,
)

# Centralized metric registry
METRICS = {
    "correlation_matrix_difference": correlation_matrix_difference,
    "frobenius_norm_difference": frobenius_norm_difference,
    "degree_difference": degree_difference,
    "strength_difference": strength_difference,
    "global_efficiency_difference": global_efficiency_difference,
}
