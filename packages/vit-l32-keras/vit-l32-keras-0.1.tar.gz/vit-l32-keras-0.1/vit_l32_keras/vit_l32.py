import tensorflow as tf


def VisionTransformer(input_shape,weight,patch_size, num_classes, hidden_dim, num_heads, mlp_dim, channels, dropout_rate):

    in_model = tf.keras.applications.EfficientNetB5(
        input_shape=(128, 128, 3),
        weights=weight,
        include_top=False
    )

    return in_model
