from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
import torch
from pydantic import BaseModel, Field
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
  bos_token='</s>', eos_token='</s>', unk_token='<unk>',
  pad_token='<pad>', mask_token='<mask>') 


model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text
        input_ids = tokenizer.encode(text)
        gen_ids = model.generate(torch.tensor([input_ids]),
                                  max_length=300,
                                  repetition_penalty=2.0,
                                  pad_token_id=tokenizer.pad_token_id,
                                  eos_token_id=tokenizer.eos_token_id,
                                  bos_token_id=tokenizer.bos_token_id,
                                  use_cache=True)
        generated = tokenizer.decode(gen_ids[0,:].tolist())

        await turn_context.send_activity(generated)

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")