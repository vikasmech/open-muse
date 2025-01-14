import torch

from muse import MaskGitTransformer, VQGANModel

codebook_size = 1024
num_classes = 1000
model = MaskGitTransformer(
    vocab_size=codebook_size + num_classes + 1,
    hidden_size=32,
    num_hidden_layers=2,
    num_attention_heads=4,
    intermediate_size=64,
    max_position_embeddings=4 + 1,  # +1 for the class token
    num_vq_tokens=4,
    codebook_size=codebook_size,
    num_classes=num_classes,
)

input_ids = torch.randint(0, 100, (1, 4))
output = model(input_ids)
assert output.shape == (1, 4, model.config.vocab_size)

class_ids = torch.tensor([1], dtype=torch.long)
gen_ids = model.generate(class_ids, timesteps=4)
assert gen_ids.shape == (1, 4)
print(gen_ids)

model.enable_gradient_checkpointing()
output = model(input_ids)
assert output.shape == (1, 4, model.config.vocab_size)


model = MaskGitTransformer(
    vocab_size=100,
    hidden_size=32,
    num_hidden_layers=2,
    num_attention_heads=4,
    intermediate_size=64,
    max_position_embeddings=4,
    add_cross_attention=True,
    encoder_hidden_size=64,
)

input_ids = torch.randint(0, 100, (1, 4))
encoder_hidden_states = torch.randn(1, 4, 64)
output = model(input_ids, encoder_hidden_states=encoder_hidden_states)
assert output.shape == (1, 4, 100)

vq = VQGANModel(
    resolution=32,
    num_channels=3,
    hidden_channels=32,
    channel_mult=(1, 2),
    num_res_blocks=2,
    attn_resolutions=tuple(),
    z_channels=64,
    num_embeddings=512,
    quantized_embed_dim=64,
)
image = torch.randn(1, 3, 32, 32)
out = vq(image)[0]
assert out.shape == (1, 3, 32, 32)
