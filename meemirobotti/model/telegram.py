from typing import ForwardRef, Optional

from pydantic import BaseModel, Field

Message = ForwardRef('Message')


class User(BaseModel):
    # https://core.telegram.org/bots/api#user
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = False
    added_to_attachment_menu: Optional[bool] = False
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None
    can_connect_to_business: Optional[bool] = None
    has_main_web_app: Optional[bool] = None
 

class Chat(BaseModel):
    # https://core.telegram.org/bots/api#chat
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[str] = None

class MessageEntity(BaseModel):
    # https://core.telegram.org/bots/api#messageentity
    type: str
    offset: int
    length: int
    url: Optional[str] = None
    user: Optional[User] = None
    language: Optional[str] = None
    custom_emoji_id: Optional[str] = None

class TextQuote(BaseModel):
    text: str
    entities: Optional[list[MessageEntity]] = None
    position: int
    is_manual: Optional[bool] = None

class Message(BaseModel):
    # https://core.telegram.org/bots/api#message
    message_id: int
    message_thread_id: Optional[int] = None
    from_: User = Field(None, alias='from')
    sender_chat: Optional[Chat] = None
    sender_boost_count: Optional[int] = None
    sender_business_bot: Optional[User] = None
    date: int
    business_connection_id: Optional[str] = None
    chat: Chat
    #forward_origin: TODO
    is_topic_message: bool = False
    is_automatic_forward: bool = False
    reply_to_message: Optional[Message] = None
    # external_reply: TODO
    quote: Optional[TextQuote] = None
    # reply_to_story: TODO
    via_bot: Optional[User] = None
    edit_date: Optional[int] = None
    has_protected_content: Optional[bool] = False
    is_from_offline: Optional[bool] = False
    media_group_id: Optional[str] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[list[MessageEntity]] = None
    # link_preview_options: TODO
    effect_id: Optional[str] = None
    # animation: TODO
    # audio: TODO
    # document: TODO
    # paid_media: TODO
    # photo: TODO
    # sticker: TODO
    # story: TODO
    # video: TODO
    # video_note: TODO
    # voice: TODO
    caption: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_media_spoiler: Optional[bool] = None
    # contact: TODO
    # dice: TODO
    # game: TODO
    # poll: TODO
    # venue: TODO
    # location: TODO
    new_chat_members: Optional[list[User]] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    # new_chat_photo: TODO
    delete_chat_photo: Optional[bool] = False
    group_chat_created: Optional[bool] = False
    supergroup_chat_created: Optional[bool] = False
    channel_chat_created: Optional[bool] = False
    delete_chat_photo: Optional[bool] = False
    # message_auto_delete_timer_changed: TODO
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    # pinned_message: TODO
    # invoice: TODO
    # successful_payment: TODO
    # refunded_payment: TODO
    # users_shared: TODO
    # chat_shared: TODO
    connected_website: Optional[str] = None
    # write_access_allowed: TODO
    # passport_data: TODO
    # proximity_alert_triggered: TODO
    # boost_added: TODO
    # chat_background_set: TODO
    # forum_topic_created: TODO
    # forum_topic_edited: TODO
    # forum_topic_closed: TODO
    # forum_topic_reopened: TODO
    # general_forum_topic_hidden: TODO
    # general_forum_topic_unhidden: TODO
    # giveaway_created: TODO
    # giveaway: TODO
    # giveaway_winners: TODO
    # giveaway_completed: TODO
    # video_chat_scheduled: TODO
    # video_chat_started: TODO
    # video_chat_ended: TODO
    # video_chat_participants_invited: TODO
    # web_app_data: TODO
    # reply_markup: TODO

class MessageId:
    # https://core.telegram.org/bots/api#messageid
    message_id: int

class InaccessibleMessage:
    # https://core.telegram.org/bots/api#inaccessiblemessage
    chat: Chat
    message_id: int
    date: int = 0

# https://core.telegram.org/bots/api#update
class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    # business_connection: TODO
    business_message: Optional[Message] = None
    edited_business_message: Optional[Message] = None
    # deleted_business_messages: TODO
    # message_reaction: TODO
    # message_reaction_count: TODO
    # inline_query: TODO
    # chosen_inline_result: TODO
    # callback_query: TODO
    # shipping_query: TODO
    # pre_checkout_query: TODO
    # poll: TODO
    # poll_answer: TODO
    # my_chat_member: TODO
    # chat_member: TODO
    # chat_join_request: TODO
    # chat_boost: TODO
    # removed_chat_boost: TODO
