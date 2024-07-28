#ifndef PQCLEAN_MCELIECE460896_CLEAN_crypto_int16_h
#define PQCLEAN_MCELIECE460896_CLEAN_crypto_int16_h

#include <inttypes.h>

#include "namespace.h"

typedef int16_t crypto_int16;

#define crypto_int16_negative_mask CRYPTO_NAMESPACE(crypto_int16_negative_mask)
crypto_int16 crypto_int16_negative_mask(crypto_int16 crypto_int16_x);
#define crypto_int16_nonzero_mask CRYPTO_NAMESPACE(crypto_int16_nonzero_mask)
crypto_int16 crypto_int16_nonzero_mask(crypto_int16 crypto_int16_x);
#define crypto_int16_zero_mask CRYPTO_NAMESPACE(crypto_int16_zero_mask)
crypto_int16 crypto_int16_zero_mask(crypto_int16 crypto_int16_x);
#define crypto_int16_positive_mask CRYPTO_NAMESPACE(crypto_int16_positive_mask)
crypto_int16 crypto_int16_positive_mask(crypto_int16 crypto_int16_x);
#define crypto_int16_unequal_mask CRYPTO_NAMESPACE(crypto_int16_unequal_mask)
crypto_int16 crypto_int16_unequal_mask(crypto_int16 crypto_int16_x, crypto_int16 crypto_int16_y);
#define crypto_int16_equal_mask CRYPTO_NAMESPACE(crypto_int16_equal_mask)
crypto_int16 crypto_int16_equal_mask(crypto_int16 crypto_int16_x, crypto_int16 crypto_int16_y);
#define crypto_int16_smaller_mask CRYPTO_NAMESPACE(crypto_int16_smaller_mask)
crypto_int16 crypto_int16_smaller_mask(crypto_int16 crypto_int16_x, crypto_int16 crypto_int16_y);
#define crypto_int16_min CRYPTO_NAMESPACE(crypto_int16_min)
crypto_int16 crypto_int16_min(crypto_int16 crypto_int16_x, crypto_int16 crypto_int16_y);
#define crypto_int16_max CRYPTO_NAMESPACE(crypto_int16_max)
crypto_int16 crypto_int16_max(crypto_int16 crypto_int16_x, crypto_int16 crypto_int16_y);
#define crypto_int16_minmax CRYPTO_NAMESPACE(crypto_int16_minmax)
void crypto_int16_minmax(crypto_int16 *crypto_int16_a, crypto_int16 *crypto_int16_b);

#endif
